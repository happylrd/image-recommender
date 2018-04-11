package io.happylrd.iris.controller;

import io.happylrd.iris.common.ServerResponse;
import io.happylrd.iris.model.Tag;
import io.happylrd.iris.repository.TagRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/tags")
public class TagController {

    @Autowired
    private TagRepository tagRepository;

    @GetMapping("/photos/{id}")
    private ServerResponse<List<Tag>> getTagsByPhoto(@PathVariable("id") Long photoId) {
        return ServerResponse.createBySuccess(tagRepository.findByPhotoId(photoId));
    }
}
