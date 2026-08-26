# 12 — JANSAHAY Transactional Outbox Notifications

## 1. Notification Outbox Pattern

To avoid partial failures during case transitions:
1. When a workflow action commits, a record is added to `notification_outbox` in the **same DB transaction**.
2. An async background task sweeps `PENDING` outbox records and delivers notifications to:
   - **In-App Notification Feed** (Citizen notification bell)
   - **Mock SMS Gateway** (Console / Log stream for demo)
   - **Mock Email Service** (Console / Log stream for demo)
3. Upon dispatch, the record is marked `PROCESSED`.
