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


@Path("/api/customers")
public class CustomerResource {

    @Inject
    public CustomerService service;

    @APIResponse(
        responseCode = "200",
        content = @Content(
            mediaType = APPLICATION_JSON,
            schema = @Schema(
                implementation = Customer.class,
                type = SchemaType.ARRAY
            )
        )
    )
    @GET
    public Response getAllCustomers(){
        List<Customer> list = service.findAllCustomers();
        return Response.ok(list).build();
    }

    @APIResponse(
        responseCode = "200",
        content = @Content(
            schema = @Schema(
                implementation = Customer.class
            )
        )
    )
    @APIResponse(
        responseCode = "204",
        description = "The customer couldn't be found by its identifier"
    )
    @GET
    @Path("/{id}")
    public Response getCustomer(@PathParam("id") Long id){
        Customer customer = service.findCustomerById(id);
        if(customer != null){
            return Response.ok(customer).build();
        }
        else
            return Response.noContent().build();
    }

    @APIResponse(
        responseCode = "201",
        description = "",
        content = @Content(
            mediaType = APPLICATION_JSON,
            schema = @Schema(
                implementation = URI.class
            )
        )
    )
    @POST
    public Response createCustomer(
        @RequestBody(
            required = true,
            content = @Content(
                mediaType = APPLICATION_JSON,
                schema = @Schema(
                    implementation = Customer.class
                )
            )
        )
        @Valid
        Customer customer,
        @Context UriInfo uriInfo ){
        customer = service.persistCustomer(customer);
        UriBuilder builder = uriInfo.getAbsolutePathBuilder().path(Long.toString(customer.id));
        return Response.created(builder.build()).build();
    }

    @APIResponse(
        responseCode="204"
    )
    @DELETE
    @Path("/{id}")
    public Response deleteCustomer(@PathParam("id") Long id){
        service.deleteCustomer(id);
        return Response.noContent().build();
    }
}