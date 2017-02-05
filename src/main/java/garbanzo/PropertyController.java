package garbanzo;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.http.HttpStatus;
import org.springframework.http.RequestEntity;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class PropertyController {
    private final Logger LOG = LoggerFactory.getLogger(this.getClass());

    @RequestMapping(value = "/properties", method = RequestMethod.POST)
    @ResponseBody
    public ResponseEntity<String> sendViaResponseEntity(RequestEntity<String> requestEntity) {
    	ResponseEntity<String> ret = new ResponseEntity<>(HttpStatus.CREATED);
    	ret.getHeaders().add("Location", "http://localhost:8080/properties/");
    	ret.getHeaders().add("Content-type", "application/json");
        return ret;
    }
    public String property(@RequestBody Property p_property) {
    	LOG.info("POST recebido");
    	Application.setNewProperty(p_property);
    	LOG.info("Imovel criado: " + p_property.getId());
    	return "{\"id\": " + p_property.getId() + "}"; 
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
