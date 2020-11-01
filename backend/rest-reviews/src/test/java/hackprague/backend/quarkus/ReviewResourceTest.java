package hackprague.backend.quarkus;

import io.quarkus.test.junit.QuarkusTest;
import org.junit.jupiter.api.Test;

import static io.restassured.RestAssured.given;
import static org.hamcrest.CoreMatchers.is;

@QuarkusTest
public class ReviewResourceTest {

    @Test
    public void testHelloEndpoint() {
        given()
          .when().get("/api/reviews")
          .then()
             .statusCode(200)
             .body(is("hello"));
    }

}