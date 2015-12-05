 CREATE TRIGGER update_OTHER_trigger AFTER UPDATE ON domain_whois_other
     FOR EACH ROW
     BEGIN
         IF NEW.flag <> -6 AND OLD.flag = -6 THEN
                         IF (SELECT count(*) from tld_whois_sum where tld = SUBSTRING_INDEX(NEW.domain,".",-1)) = 1 THEN
                                       Update tld_whois_sum SET whois_sum = whois_sum + 1 WHERE tld = SUBSTRING_INDEX(NEW.domain,".",-1) ;
                               ELSE
                                       INSERT INTO tld_whois_sum (tld,whois_sum) VALUES (SUBSTRING_INDEX(NEW.domain,".",-1),1);
                               END IF;
         END IF;
     END;