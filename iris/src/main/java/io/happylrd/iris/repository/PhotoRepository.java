package io.happylrd.iris.repository;

import io.happylrd.iris.model.Photo;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import java.util.List;

public interface PhotoRepository extends JpaRepository<Photo, Long> {

    Page<Photo> findAllByOrderByFViewNumDesc(Pageable pageable);

    // TODO: will be removed later
    @Query(value = "SELECT p.id, p.title, p.url, p.owner_id, p.f_view_num, p.f_fav_num, p.f_comment_num, p.create_time FROM photo p INNER JOIN photo_tag pt ON p.id = pt.photo_id INNER JOIN tag t ON pt.tag_id = t.id WHERE t.id = ?1", nativeQuery = true)
    List<Photo> findByTagId(Long tagId);

    @Query(value = "SELECT p.id, p.title, p.url, p.owner_id, p.f_view_num, p.f_fav_num, p.f_comment_num, p.create_time FROM photo p INNER JOIN photo_tag pt ON p.id = pt.photo_id INNER JOIN tag t ON pt.tag_id = t.id WHERE t.content = ?1", nativeQuery = true)
    List<Photo> findByTagName(String tagName);
}
