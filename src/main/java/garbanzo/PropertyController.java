package garbanzo;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.util.concurrent.atomic.AtomicLong;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class PropertyController {
    private final AtomicLong counter = new AtomicLong();
    private final Logger LOG = LoggerFactory.getLogger(this.getClass());

    @RequestMapping(value = "/properties", method = RequestMethod.POST)
    public void property(@RequestBody Property p_property) {
    	LOG.info("POST recebido");
    	Application.setNewProperty(p_property);
    	// TODO: O que retornar ao criar uma nova propriedade?
    }

    @RequestMapping(value = "/properties/{p_id}", method = RequestMethod.GET)
    public Property property(@PathVariable String p_id) {
    	LOG.info("GET recebido");
    	Property ret = Application.getSpecificProperty(p_id);
    	
    	if (ret != null) {
    		LOG.info("Encontrou!");
    		return ret;
    	} else {
    		LOG.warn("Não encontrou!");
    		return null; // TODO: 404?
    	}
    }

    @RequestMapping(value = "/properties", method = RequestMethod.GET)
    public Property property(@RequestParam("ax") int p_ax, @RequestParam("ay") int p_ay, @RequestParam("bx") int p_bx, @RequestParam("by") int p_by) {
    	LOG.info("GET recebido");
   		return null; // TODO: Construir a pesquisa.
    }
}
