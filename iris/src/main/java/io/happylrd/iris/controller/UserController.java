package io.happylrd.iris.controller;

import io.happylrd.iris.common.ServerResponse;
import io.happylrd.iris.model.Photo;
import io.happylrd.iris.model.User;
import io.happylrd.iris.model.UserPhotoRec;
import io.happylrd.iris.repository.PhotoRepository;
import io.happylrd.iris.repository.UserPhotoRecRepository;
import io.happylrd.iris.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

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

//    @PostMapping("/login")
//    private ServerResponse<User> login(User user) {
//        long resultCount = userRepository.countByUsername(user.getUsername());
//        if (resultCount == 0) {
//            return ServerResponse.createByErrorMessage("用户名不存在");
//        }
//
//        User userInst = userRepository.findByUsernameAndPassword(user.getUsername(), user.getPassword());
//        if (userInst == null) {
//            return ServerResponse.createByErrorMessage("密码错误");
//        }
//        return ServerResponse.createBySuccess("登录成功", userInst);
//    }

    @GetMapping("/{username}")
    private ServerResponse<User> getInfo(@PathVariable("username") String username) {
        return ServerResponse.createBySuccess(userRepository.findByUsername(username));
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
