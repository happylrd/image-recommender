package io.happylrd.iris.model;

import javax.persistence.*;
import java.time.LocalDateTime;

@Entity
public class Photo {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column
    private String title;

    @Column
    private String url;

    @ManyToOne
    @JoinColumn(name = "owner_id", nullable = false)
    private User owner;

    @Column
    private LocalDateTime createTime = LocalDateTime.now();
}
