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

import jdk.jfr.Description;


import static javax.ws.rs.core.MediaType.APPLICATION_JSON;

import java.net.URI;
import java.util.List;
import javax.inject.Inject;
import javax.validation.Valid;

@Path("/api/reviews")
public class ReviewResource {

    @Inject
    public ReviewService service;

    @APIResponse(
        responseCode = "200",
        content = @Content(
            mediaType = APPLICATION_JSON,
            schema = @Schema(
                implementation = Review.class,
                type = SchemaType.ARRAY
            )
        )
    )
    @GET
    public Response getAllReviews(){
        List<Review> reviews = service.findAllReviews();
        return Response.ok(reviews).build();
    }

    
    @APIResponse(
        responseCode = "200",
        content = @Content(
            schema = @Schema(
                implementation = Review.class
            )
        )
    )
    @APIResponse(
        responseCode = "204",
        description = "No reviews with following identifier was found"
    )
    @GET
    @Path("/{id}")
    public Response getReview(@PathParam("id") Long id){
        Review review = service.findReviewById(id);
        if(review != null){
            return Response.ok(review).build();
        }
        else{
            return Response.noContent().build();
        }
    }
    
    @APIResponse(
        responseCode = "201",
        content  = @Content(
            mediaType = APPLICATION_JSON,
            schema = @Schema(
                implementation = URI.class
            )
        )
    )
    @POST
    public Response createReview(
        @RequestBody(
            required = true,
            content = @Content(
                mediaType = APPLICATION_JSON,
                schema = @Schema(
                    implementation = Review.class
                )
            )
        )
        @Valid
        Review review, 
        @Context
        UriInfo uriInfo ) {
            review = service.persistReview(review);
            UriBuilder builder = uriInfo.getAbsolutePathBuilder().path(Long.toString(review.id));
            //todo: call /api/checkReview
            return Response.created(builder.build()).build();
    }

    @APIResponse(
        responseCode = "204"
    )
    @DELETE
    @Path("/{id}")
    public Response deleteReview(@PathParam("id") Long id){
        service.deleteReview(id);
        return Response.noContent().build();
    }
}