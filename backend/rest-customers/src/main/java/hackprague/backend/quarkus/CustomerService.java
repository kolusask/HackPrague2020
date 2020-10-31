package hackprague.backend.quarkus;

import javax.enterprise.context.ApplicationScoped;
import javax.transaction.Transactional;
import javax.validation.Valid;

import hackprague.backend.quarkus.Customer;

import static javax.transaction.Transactional.TxType.REQUIRED;
import static javax.transaction.Transactional.TxType.SUPPORTS;
import java.util.List;

@ApplicationScoped
@Transactional(REQUIRED)
public class CustomerService {
    @Transactional(SUPPORTS)
    public List<Customer>findAllCustomers(){
        return Customer.listAll();
    }

    @Transactional(SUPPORTS)
    public Customer findCustomerById(Long id){
        return Customer.findById(id);
    }

    public Customer persistCustomer(@Valid Customer customer){
        Customer.persist(customer);
        return customer;
    }

    public Customer updateCustomer(@Valid Customer customer){
        Customer entity = Customer.findById(customer.id);

        entity.email = customer.email;
        entity.subcategoriesList= customer.subcategoriesList;
        entity.category = customer.category;
        entity.isCompany = customer.isCompany;
        entity.isFreelancer = customer.isFreelancer;
        entity.firstName = customer.firstName;
        entity.lastName = customer.lastName;
        entity.Reviewee = customer.Reviewee;
        entity.Reviewer = customer.Reviewer;

        return entity;
    }

    public void deleteCustomer(Long id){
        Customer customer = Customer.findById(id);
        customer.delete();
    }
}
