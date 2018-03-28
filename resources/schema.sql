CREATE SCHEMA jars WITH OWNER jars;

SET search_path TO jars, public;

CREATE TABLE events (
	event_uuid UUID NOT NULL PRIMARY KEY,
	created_time TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL,
	created_by INTEGER NOT NULL,
	connected BOOLEAN DEFAULT FALSE NOT NULL,
	connected_by INTEGER,
	title VARCHAR(255),
	description VARCHAR(255),
	# If private, should not be shown on public-facing sites (e.g. OS returns to studio)
	private BOOLEAN DEFAULT FALSE NOT NULL,
	# Could be used to link to a Show/Season/Timeslot in future
	relation_id INTEGER
);
