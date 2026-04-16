package example.demo;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;
import java.util.HashMap;
import java.util.Map;

@RestController
public class AiController {

    @GetMapping("/hello")
    public String sayHello() {
        return "FlexiSAF Bridge: System Online!";
    }

    @PostMapping("/ai-query")
    public String callAi(@RequestBody String userQuestion) {
        RestTemplate restTemplate = new RestTemplate();
        // Pointing to your Python FastAPI server
        String pythonUrl = "http://127.0.0.1:8000/ask"; 

        Map<String, String> requestBody = new HashMap<>();
        requestBody.put("question", userQuestion);

        try {
            Map<String, Object> response = restTemplate.postForObject(pythonUrl, requestBody, Map.class);
            return response.get("agent_response").toString();
        } catch (Exception e) {
            return "Error: Java could not reach the Python AI service at " + pythonUrl;
        }
    }
}