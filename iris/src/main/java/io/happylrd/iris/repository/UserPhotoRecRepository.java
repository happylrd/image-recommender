package io.happylrd.iris.repository;

import io.happylrd.iris.model.UserPhotoRec;
import org.springframework.data.jpa.repository.JpaRepository;

public interface UserPhotoRecRepository extends JpaRepository<UserPhotoRec, Long> {

    UserPhotoRec findByUserId(Long userId);
}
