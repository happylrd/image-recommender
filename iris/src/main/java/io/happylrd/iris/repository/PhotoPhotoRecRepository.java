package io.happylrd.iris.repository;

import io.happylrd.iris.model.PhotoPhotoRec;
import org.springframework.data.jpa.repository.JpaRepository;

public interface PhotoPhotoRecRepository extends JpaRepository<PhotoPhotoRec, Long> {

    PhotoPhotoRec findByPhotoId(Long photoId);
}
