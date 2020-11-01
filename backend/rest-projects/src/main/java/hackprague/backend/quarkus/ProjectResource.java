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
//import org.graalvm.compiler.graph.Node.InjectedNodeParameter;

import jdk.jfr.ContentType;
import jdk.jfr.Description;


import static javax.ws.rs.core.MediaType.APPLICATION_JSON;

import java.net.URI;
import java.util.List;
import javax.inject.Inject;
import javax.validation.Valid;

@Path("/api/projects")
public class ProjectResource {

    @Inject
    ProjectService service;


    @APIResponse(
        responseCode = "200",
        content = @Content(
            mediaType = APPLICATION_JSON,
            schema = @Schema(
                implementation = Project.class,
                type = SchemaType.ARRAY
            )
        )
    )
    @GET
    public Response getAllProjects(){
        List<Project> list = service.findAllProjects();
        return Response.ok(list).build();
    }

    @APIResponse(
        responseCode = "200",
        content = @Content(
            schema = @Schema(
                implementation = Project.class
            )
        )
    )
    @APIResponse(
        responseCode = "204",
        description = "The project with specific identifier was not found"
    )
    @GET
    @Path("/{id}")
    public Response getProjectById(@PathParam("id") Long id){
        Project project = service.findProjectById(id);
        if(project != null){
            return Response.ok(project).build();
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
    public Response createProject(
        @RequestBody(
            required = true,
            content = @Content(
                mediaType = APPLICATION_JSON,
                schema = @Schema(
                    implementation = Project.class
                )
            )
        )
        @Valid
        Project project, 
        @Context UriInfo uriInfo){
            project = service.persistProject(project);
            UriBuilder builder = uriInfo.getAbsolutePathBuilder().path(Long.toString(project.id));
            return Response.created(builder.build()).build();
        }

    @APIResponse(
        responseCode = "204"
    )
    @DELETE
    @Path("/{id}")
    public Response deleteProject(@PathParam("id") Long id){
        service.deleteProject(id);
        return Response.noContent().build();
    }
    
}