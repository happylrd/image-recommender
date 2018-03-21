package io.happylrd.iris.model;

import javax.persistence.*;
import java.time.LocalDateTime;

@Entity
public class PhotoTag {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne
    @JoinColumn(name = "photo_id", nullable = false)
    private Photo photo;

    @ManyToOne
    @JoinColumn(name = "tag_id", nullable = false)
    private Tag tag;

    @Column
    private LocalDateTime createTime = LocalDateTime.now();
}
