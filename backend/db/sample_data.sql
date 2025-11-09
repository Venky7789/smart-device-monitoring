INSERT INTO companies (name) VALUES ('Alpha Corp') ON CONFLICT DO NOTHING;
INSERT INTO companies (name) VALUES ('Beta Ltd') ON CONFLICT DO NOTHING;

INSERT INTO devices (name, company_id)
SELECT 'Alpha-Device-1', id FROM companies WHERE name='Alpha Corp' ON CONFLICT DO NOTHING;
INSERT INTO devices (name, company_id)
SELECT 'Alpha-Device-2', id FROM companies WHERE name='Alpha Corp' ON CONFLICT DO NOTHING;

INSERT INTO devices (name, company_id)
SELECT 'Beta-Device-1', id FROM companies WHERE name='Beta Ltd' ON CONFLICT DO NOTHING;

-- recent reading (online)
INSERT INTO device_readings (device_id, timestamp)
SELECT d.id, NOW() FROM devices d WHERE d.name = 'Alpha-Device-1';

-- old reading (offline)
INSERT INTO device_readings (device_id, timestamp)
SELECT d.id, NOW() - INTERVAL '10 minutes' FROM devices d WHERE d.name = 'Alpha-Device-2';
