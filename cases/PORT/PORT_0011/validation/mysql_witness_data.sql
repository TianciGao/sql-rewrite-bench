-- DRAFT witness data only; not executed in this task
INSERT INTO event (event_id, event_name) VALUES
  (1, 'Deep Deficit Gala'),
  (2, 'Small Deficit Gala');
INSERT INTO budget (link_to_event, event_status, remaining) VALUES
  (1, 'Closed', -50.0),
  (2, 'Closed', -5.0);
