package io.happylrd.iris.model;

import javax.persistence.*;
import java.time.LocalDateTime;

@Entity
public class Tag {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column
    private String raw;

    @Column
    private String content;

    @Column
    private LocalDateTime createTime = LocalDateTime.now();
}
