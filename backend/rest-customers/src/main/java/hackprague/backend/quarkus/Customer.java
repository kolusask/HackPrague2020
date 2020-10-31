package hackprague.backend.quarkus;

import io.quarkus.hibernate.orm.panache.PanacheEntityBase;

import java.util.List;
import java.util.Set;

import javax.persistence.Entity;
import javax.persistence.Column;
import javax.persistence.OneToMany;

import javax.validation.constraints.NotNull;

@Entity
public class Customer extends PanacheEntityBase{
    
    @Id
    @Column(name = "customerID")
    public Long customerID;
    
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

    @OneToMany(mappedBy = "customer", orphanRemoval=true)
    public Set<Review> Reviewer;
    
    @OneToMany(mappedBy = "customer", orphanRemoval=true)
    public Set<Review> Reviewee;

    @Override
    public String toString(){
        return firstName + " " + lastName + "(" + email + ")";
    }

}
