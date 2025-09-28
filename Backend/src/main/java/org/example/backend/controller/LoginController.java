package org.example.backend.controller;


import lombok.extern.slf4j.Slf4j;
import org.example.backend.pojo.LoginPo;
import org.example.backend.pojo.RegisterPo;
import org.example.backend.pojo.Result;
import org.example.backend.pojo.guestResult;
import org.example.backend.service.LoginService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@Slf4j
@RequestMapping("/api/auth")
public class LoginController {

    @Autowired
    private LoginService loginService;


    //登录接口
    @PostMapping("/login")
    public Result login(@RequestBody LoginPo po) {
        return loginService.login(po);
    }

    //注册接口
    @PostMapping("/register")
    public Result register(@RequestBody RegisterPo po) {
        return loginService.register(po);
    }

    //游客登录
    @PostMapping("/guest")
    public guestResult guest(){
        return loginService.guest();
    }

}
