package hackprague.backend.quarkus;

import javax.ws.rs.*;
import javax.ws.rs.core.Context;
import javax.ws.rs.core.Response;
import javax.ws.rs.core.UriBuilder;
import javax.ws.rs.core.UriInfo;

import org.eclipse.microprofile.openapi.annotations.Operation;
import org.eclipse.microprofile.openapi.annotations.enums.SchemaType;
import org.eclipse.microprofile.openapi.annotations.media.Content;
import org.eclipse.microprofile.openapi.annotations.media.Schema;
import org.eclipse.microprofile.openapi.annotations.parameters.Parameter;
import org.eclipse.microprofile.openapi.annotations.parameters.RequestBody;
import org.eclipse.microprofile.openapi.annotations.responses.APIResponse;

import static javax.ws.rs.core.MediaType.APPLICATION_JSON;

import java.net.URI;
import java.util.List;
import javax.inject.Inject;
import javax.validation.Valid;

@Path("/api/orders")
public class OrderResource {

    @Inject 
    OrderService service;

    @APIResponse(
        responseCode = "200",
        content = @Content(
            mediaType = APPLICATION_JSON,
            schema = @Schema(
                implementation = Order.class,
                type = SchemaType.ARRAY
            )
        )
    )
    @GET
    public Response getAllOrders(){
        List<Order> orders = service.findAllOrders();
        return Response.ok(orders).build();
    }

    @APIResponse(
        responseCode = "200",
        content = @Content(
            mediaType = APPLICATION_JSON,
            schema = @Schema(
                implementation = Order.class
            )
        )
    )
    @APIResponse(
        responseCode = "204",
        description = "There wasn't any order with identifier reequested"
    )
    @GET
    @Path("/{id}")
    public Response getOrder(@PathParam("id") Long id){
        Order order = service.findOrderById(id);
        if(order != null){
            return Response.ok(order).build();
        }
        else{
            return Response.noContent().build();
        }
    }
    
    
    @APIResponse(
        responseCode = "201",
        content = @Content(
            mediaType = APPLICATION_JSON,
            schema = @Schema(
                implementation = URI.class
            )
        )
    )
    @POST
    public Response crateOrder(
        @RequestBody(
            required = true,
            content = @Content(
                mediaType = APPLICATION_JSON,
                schema = @Schema(
                    implementation = Order.class
                )
            )
        )
        @Valid Order order,
        @Context UriInfo uriInfo){
            order = service.persistOrder(order);
            UriBuilder builder = uriInfo.getAbsolutePathBuilder().path(Long.toString(order.id));
            return Response.created(builder.build()).build();
    }

    @APIResponse(
        responseCode = "204"
    )
    @DELETE
    @Path("/{id}")
    public Response deleteOrder(@PathParam("id") Long id){
        service.deleteOrder(id);
        return Response.noContent().build();
    }
}