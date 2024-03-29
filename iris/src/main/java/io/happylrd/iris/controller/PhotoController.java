package io.happylrd.iris.controller;

import io.happylrd.iris.common.ServerResponse;
import io.happylrd.iris.model.Photo;
import io.happylrd.iris.model.PhotoPhotoRec;
import io.happylrd.iris.repository.PhotoPhotoRecRepository;
import io.happylrd.iris.repository.PhotoRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/photos")
public class PhotoController {

    @Autowired
    private PhotoRepository photoRepository;

    @Autowired
    private PhotoPhotoRecRepository photoPhotoRecRepository;

    @GetMapping
    private ServerResponse<Page<Photo>> getHotPhotos(@RequestParam(value = "pageNum") Integer pageNum,
                                                     @RequestParam(value = "pageSize") Integer pageSize) {
        Page<Photo> photoList = photoRepository
                .findAllByOrderByFViewNumDesc(PageRequest.of(pageNum, pageSize));
        return ServerResponse.createBySuccess(photoList);
    }

    @GetMapping("/newest")
    private ServerResponse<Page<Photo>> getNewestPhotos(@RequestParam(value = "pageNum") Integer pageNum,
                                                        @RequestParam(value = "pageSize") Integer pageSize) {
        Page<Photo> photoList = photoRepository
                .findAllByOrderByCreateTimeDesc(PageRequest.of(pageNum, pageSize));
        return ServerResponse.createBySuccess(photoList);
    }

    @GetMapping("/{id}")
    private ServerResponse<Photo> get(@PathVariable("id") Long photoId) {
        return ServerResponse.createBySuccess(photoRepository.findById(photoId).get());
    }

    @GetMapping("/rec/{id}")
    private ServerResponse<List<Photo>> getRecPhotos(@PathVariable("id") Long photoId) {
        PhotoPhotoRec photoPhotoRec = photoPhotoRecRepository.findByPhotoId(photoId);
        List<Long> recPhotoIds = Arrays.stream(photoPhotoRec.getRecPhotoIds().split(","))
                .map(Long::parseLong)
                .collect(Collectors.toList());

        List<Photo> photos = new ArrayList<>();
        for (Long recPhotoId : recPhotoIds) {
            photos.add(photoRepository.findById(recPhotoId).get());
        }
        return ServerResponse.createBySuccess(photos);
    }

    @GetMapping("/tags/{name}")
    private ServerResponse<List<Photo>> getPhotosByTag(@PathVariable("name") String tagName) {
        return ServerResponse.createBySuccess(photoRepository.findByTagName(tagName));
    }
}
