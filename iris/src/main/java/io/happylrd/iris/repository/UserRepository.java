package io.happylrd.iris.repository;

import io.happylrd.iris.model.User;
import org.springframework.data.jpa.repository.JpaRepository;

public interface UserRepository extends JpaRepository<User, Long> {

    Long countByUsername(String username);

    User findByUsernameAndPassword(String username, String password);
}
