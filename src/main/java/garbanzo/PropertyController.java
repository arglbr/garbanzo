package garbanzo;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.util.concurrent.atomic.AtomicLong;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class PropertyController {
    private final AtomicLong counter = new AtomicLong();
    private final Logger logger = LoggerFactory.getLogger(this.getClass());

    @RequestMapping(value = "/properties", method = RequestMethod.GET)
    public Property property(@RequestParam(value="id", defaultValue="*") String p_id) {
	logger.info("GET recebido");
        return new Property();
    }

    @RequestMapping(value = "/properties", method = RequestMethod.POST)
    public Property property(@RequestBody Property p_property) {
	logger.info("POST recebido");
        return new Property();
    }
}
