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
    private Integer fViewNum;

    @Column
    private Integer fFavNum;

    @Column
    private Integer fCommentNum;

    @Column
    private LocalDateTime createTime = LocalDateTime.now();

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = url;
    }

    public User getOwner() {
        return owner;
    }

    public void setOwner(User owner) {
        this.owner = owner;
    }

    public Integer getFViewNum() {
        return fViewNum;
    }

    public void setFViewNum(Integer fViewNum) {
        this.fViewNum = fViewNum;
    }

    public Integer getFFavNum() {
        return fFavNum;
    }

    public void setFFavNum(Integer fFavNum) {
        this.fFavNum = fFavNum;
    }

    public Integer getFCommentNum() {
        return fCommentNum;
    }

    public void setFCommentNum(Integer fCommentNum) {
        this.fCommentNum = fCommentNum;
    }

    public LocalDateTime getCreateTime() {
        return createTime;
    }

    public void setCreateTime(LocalDateTime createTime) {
        this.createTime = createTime;
    }
}
