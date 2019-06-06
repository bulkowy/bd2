CREATE FUNCTION log_sub() RETURNS trigger as $log_sub$
	DECLARE
		sbdpos_id 	INTEGER;
		sbgpos_id	INTEGER;
	BEGIN
		SELECT position_id INTO sbdpos_id FROM app_worker WHERE id = NEW.substituted_worker_id;
		SELECT position_id INTO sbgpos_id FROM app_worker WHERE id = NEW.substituting_worker_id;
		INSERT INTO app_logentry (substitute_begin, substitute_end, subbed_id, subbing_id, reason_id, old_position_id, new_position_id) 
		VALUES(NEW.substitute_begin, NEW.substitute_end, NEW.substituted_worker_id, NEW.substituting_worker_id, 2, sbdpos_id, sbgpos_id);
		RETURN NEW;
	END;
$log_sub$ LANGUAGE plpgsql;

CREATE TRIGGER log_sub AFTER INSERT ON app_substitution
	FOR EACH ROW EXECUTE PROCEDURE log_sub();

CREATE FUNCTION log_sub2() RETURNS trigger as $log_sub2$
	BEGIN
		IF NEW.position_id != OLD.position_id THEN
			INSERT INTO app_logentry (substitute_begin, substitute_end, subbed_id, subbing_id, reason_id, old_position_id, new_position_id)
			VALUES(NEW.promotion_date, null, NEW.id, null, 1, OLD.position_id, NEW.position_id);
		END IF;
		RETURN NEW;
	END;
$log_sub2$ LANGUAGE plpgsql;

CREATE TRIGGER log_sub2 AFTER UPDATE ON app_worker
	FOR EACH ROW EXECUTE PROCEDURE log_sub2();
