package io.happylrd.iris.repository;

import io.happylrd.iris.model.Tag;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import java.util.List;

public interface TagRepository extends JpaRepository<Tag, Long> {

    @Query(value = "SELECT t.id, t.raw, t.content, t.create_time FROM tag t INNER JOIN photo_tag pt ON t.id = pt.tag_id INNER JOIN photo p ON pt.photo_id = p.id WHERE p.id = ?1", nativeQuery = true)
    List<Tag> findByPhotoId(Long photoId);
}
