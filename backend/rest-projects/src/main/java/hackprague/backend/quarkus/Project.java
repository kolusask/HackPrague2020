package hackprague.backend.quarkus;

import io.quarkus.hibernate.orm.panache.PanacheEntity;

import java.util.List;

import javax.persistence.Entity;


import javax.validation.constraints.NotNull;


@Entity
public class Project extends PanacheEntity{
    @NotNull
    public String Title;

    @NotNull
    public String Description;

    @NotNull
    public String Category;

    @Override
    public String toString(){
        return Title + ": " + Description + " (" + Category + ")";
    }
}
