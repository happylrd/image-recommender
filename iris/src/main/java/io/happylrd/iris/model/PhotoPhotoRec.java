package io.happylrd.iris.model;

import javax.persistence.*;
import java.time.LocalDateTime;

@Entity
public class PhotoPhotoRec {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(unique = true, nullable = false)
    private Long photoId;

    @Column
    private String recPhotoIds;

    @Column
    private LocalDateTime createTime = LocalDateTime.now();
}
