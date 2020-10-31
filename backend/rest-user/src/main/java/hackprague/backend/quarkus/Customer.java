package hackprague.backend.quarkus;

import io.quarkus.hibernate.orm.panache.PanacheEntity;

import java.util.List;

import javax.persistence.Entity;
import javax.validation.constraints.NotNull;

@Entity
public class Customer extends PanacheEntity{
    @NotNull
    public String firstName;

    @NotNull
    public String lastName;

    @NotNull
    public String email;

    @NotNull
    public Boolean isFreelancer;

    @NotNull
    public Boolean isCompany;

    @NotNull
    public String category;
    
    @NotNull
    public List<String> subcategoriesList;

    @Override
    public String toString(){
        return firstName + " " + lastName + "(" + email + ")";
    }

}
