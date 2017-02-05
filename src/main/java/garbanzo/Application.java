package garbanzo;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import javax.annotation.PostConstruct;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;

@SpringBootApplication
public class Application {
    private final Logger LOG = LoggerFactory.getLogger(this.getClass());
	private static ArrayList<Property> properties = new ArrayList<Property>();

	@PostConstruct
    public void init() throws IOException {
    	ObjectMapper mapper = new ObjectMapper();

        try {
			properties = mapper.readValue(loadJsonFile(), new TypeReference<ArrayList<Property>>(){});
			LOG.info("Dados de imoveis carregados.");
		} catch (IOException e) {
			LOG.error("Um erro ocorreu ao carregar os dados de imoveis. Detalhes: " + e.getMessage());
		}
    }

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }

    private static File loadJsonFile() {
        return new File("/home/arglbr/src/arglbr/garbanzo/data/properties.json");
    }
    
    public static ArrayList<Property> getProperties() {
    	return properties;
    }

    public static int getNumberOfProperties() {
    	return properties.size();
    }

    public static void setNewProperty(Property p_prop) {
    	properties.add(p_prop);
    }
}
