package io.happylrd.iris.controller;

import io.happylrd.iris.common.ServerResponse;
import io.happylrd.iris.model.Photo;
import io.happylrd.iris.model.User;
import io.happylrd.iris.model.UserPhotoRec;
import io.happylrd.iris.repository.PhotoRepository;
import io.happylrd.iris.repository.UserPhotoRecRepository;
import io.happylrd.iris.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/users")
public class UserController {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private UserPhotoRecRepository userPhotoRecRepository;

    @Autowired
    private PhotoRepository photoRepository;

    @GetMapping("/login")
    private ServerResponse<User> login(String username, String password) {
        long resultCount = userRepository.countByUsername(username);
        if (resultCount == 0) {
            return ServerResponse.createByErrorMessage("用户名不存在");
        }

        User user = userRepository.findByUsernameAndPassword(username, password);
        if (user == null) {
            return ServerResponse.createByErrorMessage("密码错误");
        }
        return ServerResponse.createBySuccess("登录成功", user);
    }

    @GetMapping("/rec/{id}")
    private ServerResponse<List<Photo>> getRecPhotos(@PathVariable("id") Long userId) {
        UserPhotoRec userPhotoRec = userPhotoRecRepository.findByUserId(userId);
        List<Long> recPhotoIds = Arrays.stream(userPhotoRec.getRecPhotoIds().split(","))
                .map(Long::parseLong)
                .collect(Collectors.toList());

        List<Photo> photos = new ArrayList<>();
        for (Long photoId : recPhotoIds) {
            photos.add(photoRepository.findById(photoId).get());
        }
        return ServerResponse.createBySuccess(photos);
    }
}
