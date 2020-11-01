package hackprague.backend.quarkus;

import javax.enterprise.context.ApplicationScoped;
import javax.transaction.Transactional;
import javax.validation.Valid;

import hackprague.backend.quarkus.Project;
//import hackprague.backend.quarkus.Review;

import static javax.transaction.Transactional.TxType.REQUIRED;
import static javax.transaction.Transactional.TxType.SUPPORTS;
import java.util.List;

@ApplicationScoped
@Transactional(REQUIRED)
public class ProjectService {
    @Transactional(SUPPORTS)
    public List<Project> findAllProjects(){
        return Project.listAll();
    }

    @Transactional(SUPPORTS)
    public Project findProjectById(Long id){
        return Project.findById(id);
    }

    public Project persistProject(@Valid Project project){
        Project.persist(project);
        return project;
    }

    public Project updateProject(@Valid Project project){
        Project entity = Project.findById(project.id);
        entity.Category = project.Category;
        entity.Description = project.Description;
        entity.Title = project.Title;

        return entity;
    }

    public void deleteProject(Long id){
        Project project = Project.findById(id);
        project.delete();
    }
}
