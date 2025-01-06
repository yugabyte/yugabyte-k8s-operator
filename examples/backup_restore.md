# YugabyteDB Backup Guide Using Kubernetes Operator

This guide outlines the steps to perform a backup using the YugabyteDB Kubernetes Operator:
  * Create a storage configuration.
  * Set up a test database and table.
  * Apply a backup Custom Resource (CR) to back up the data.
  * Apply a restoreJob Custom Resource (CR) to restore the data in a different DB
```yaml
# Create Storage Configuration
apiVersion: operator.yugabyte.io/v1alpha1
kind: StorageConfig
metadata:
  name: s3-config-operator
  namespace: operator-test
spec:
  config_type: STORAGE_S3
  data:
    AWS_ACCESS_KEY_ID: <your-access-key>
    AWS_SECRET_ACCESS_KEY: <your-secret-key>
    BACKUP_LOCATION: s3://backups.yugabyte.com/s3Backup

```
# Apply the storage configuration
```
kubectl apply -f ~/crs/testStorageConfigCr.yaml -n operator-test
```

# Access the Yugabyte TServer pod
```
kubectl exec -it -n operator-test <yb-tserver-pod-name> -- /bin/bash
```
# Create a Test Database and Table
```sql
# Once inside the pod, use `ysqlsh` to create a test database and table
CREATE DATABASE testdb;
\c testdb

CREATE TABLE test_table (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO test_table (name, age) VALUES
('Alice', 30),
('Bob', 25),
('Charlie', 35);

SELECT * FROM test_table;

```

# Create a Backup Custom Resource

```yaml
apiVersion: operator.yugabyte.io/v1alpha1
kind: Backup
metadata:
  name: operator-backup
  namespace: operator-test
spec:
  backupType: PGSQL_TABLE_TYPE
  keyspace: testdb
  storageConfig: s3-config-operator
  timeBeforeDelete: 1234567890
  universe: operator-test
```
# Apply Backup CR
```
kubectl apply -f ~/crs/testBackupDemo.yaml  -n operator-test
```
  
# Verifying StorageConfig and Backup CR Status

```yaml
# Check the StorageConfig Status
kubectl get storageconfig -n operator-test -o yaml

# Example Output
apiVersion: v1
items:
- apiVersion: operator.yugabyte.io/v1alpha1
  kind: StorageConfig
  metadata:
    name: s3-config-operator
    namespace: operator-test
  spec:
    config_type: STORAGE_S3
    data:
      AWS_ACCESS_KEY_ID: <your-access-key>
      AWS_SECRET_ACCESS_KEY: <your-secret-key>
      BACKUP_LOCATION: s3://backups.yugabyte.com/s3Backup
  status:
    message: Updated Storage Config
    success: true

# Validate that "success" is true in the `status` section.
```
# Check the Backup CR Status
```yaml
kubectl get backups -n operator-test -o yaml

# Example Output
apiVersion: v1
items:
- apiVersion: operator.yugabyte.io/v1alpha1
  kind: Backup
  metadata:
    name: operator-backup
    namespace: operator-test
  spec:
    backupType: PGSQL_TABLE_TYPE
    keyspace: testdb
    storageConfig: s3-config-operator
    timeBeforeDelete: 1234567890
    universe: operator-test
  status:
    message: 'Backup State: Completed'
    resourceUUID: e84c0960-3038-49db-9729-d649c4ca8b52
    taskUUID: 76fd2627-19fc-411b-9661-32c9d1f26588
```
Ensure the `status.message` field shows "Backup State: Completed".

# Restore the backup to the same universe
```
[centos@dev-server-anijhawan-4 yugabyte-k8s-operator]$ cat  ~/crs/testRestoreDemo.yaml 
```
```yaml
apiVersion: operator.yugabyte.io/v1alpha1
kind: RestoreJob
metadata:
  name: operator-restore-5
spec:
  actionType: RESTORE
  universe: operator-test # Name of universe CR
  backup: operator-backup # Name of backup CR
  keyspace: pg_restore  # Name of the keyspace/table to restore into
```

# Check restore status 
```yaml
[centos@dev-server-anijhawan-4 yugabyte-k8s-operator]$ kubectl get restorejobs -n operator-test -o yaml  
apiVersion: v1
items:
- apiVersion: operator.yugabyte.io/v1alpha1
  kind: RestoreJob
  metadata:
    annotations:
      kubectl.kubernetes.io/last-applied-configuration: |
        {"apiVersion":"operator.yugabyte.io/v1alpha1","kind":"RestoreJob","metadata":{"annotations":{},"name":"operator-restore-5","namespace":"operator-test"},"spec":{"actionType":"RESTORE","backup":"operator-backup","keyspace":"pg_restore","universe":"operator-test"}}
    creationTimestamp: "2025-01-06T22:38:54Z"
    generation: 1
    name: operator-restore-5
    namespace: operator-test
    resourceVersion: "982809493"
    uid: af7a692c-7744-48fe-956b-f2c96ef0c3e5
  spec:
    actionType: RESTORE
    backup: operator-backup
    keyspace: pg_restore
    universe: operator-test
  status:
    message: scheduled restoreJob task
    taskUUID: 3e72f164-3d71-45e9-b64c-d121f8db0cb8
kind: List
metadata:
  resourceVersion: ""
```

# Completed Restore
```yaml
[centos@dev-server-anijhawan-4 yugabyte-k8s-operator]$ kubectl get restorejobs -n operator-test -o yaml  
apiVersion: v1
items:
- apiVersion: operator.yugabyte.io/v1alpha1
  kind: RestoreJob
  metadata:
    annotations:
      kubectl.kubernetes.io/last-applied-configuration: |
        {"apiVersion":"operator.yugabyte.io/v1alpha1","kind":"RestoreJob","metadata":{"annotations":{},"name":"operator-restore-5","namespace":"operator-test"},"spec":{"actionType":"RESTORE","backup":"operator-backup","keyspace":"pg_restore","universe":"operator-test"}}
    creationTimestamp: "2025-01-06T22:38:54Z"
    generation: 1
    name: operator-restore-5
    namespace: operator-test
    resourceVersion: "982809909"
    uid: af7a692c-7744-48fe-956b-f2c96ef0c3e5
  spec:
    actionType: RESTORE
    backup: operator-backup
    keyspace: pg_restore
    universe: operator-test
  status:
    message: Finished Restore
    taskUUID: 3e72f164-3d71-45e9-b64c-d121f8db0cb8
kind: List
metadata:
  resourceVersion: ""
```

