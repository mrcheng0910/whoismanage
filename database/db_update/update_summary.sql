CREATE TRIGGER update_summary_trigger AFTER INSERT ON domain_update
		FOR EACH ROW
     BEGIN
				 IF (SELECT count(*) from domain_summary where tld_name = NEW.tld_name) = 1 THEN
						 Update domain_summary SET domain_num = NEW.domain_num, query_time = NEW.update_time WHERE tld_name = NEW.tld_name ;
				 ELSE
						 INSERT INTO domain_summary (tld_name, domain_num, query_date) VALUES (NEW.tld_name,NEW.domain_num, NEW.update_time);
				 END IF;
     END;
