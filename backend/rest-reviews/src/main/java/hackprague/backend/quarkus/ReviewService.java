package hackprague.backend.quarkus;

import javax.enterprise.context.ApplicationScoped;
import javax.transaction.Transactional;
import javax.validation.Valid;

import hackprague.backend.quarkus.Review;

import static javax.transaction.Transactional.TxType.REQUIRED;
import static javax.transaction.Transactional.TxType.SUPPORTS;
import java.util.List;


@ApplicationScoped
@Transactional(REQUIRED)
public class ReviewService {

    @Transactional(SUPPORTS)
    public List<Review> findAllReviews(){
        return Review.listAll();
    }

    @Transactional(SUPPORTS)
    public Review findReviewById(Long id){
        return Review.findById(id);
    }

    public Review persistReview(@Valid Review review){
        Review.persist(review);
        return review;
    }

    public Review updateReview(@Valid Review review){
        Review entity = Review.findById(review.id);

        entity.Mark = review.Mark;
        entity.Text = review.Text;

        return entity;
    }

    public void deleteReview(Long id){
        Review review = Review.findById(id);
        review.delete();
    }
    
}
