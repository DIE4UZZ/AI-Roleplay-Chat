package org.example.backend.controller;


import lombok.extern.slf4j.Slf4j;
import org.example.backend.pojo.LoginPo;
import org.example.backend.pojo.RegisterPo;
import org.example.backend.pojo.Result;
import org.example.backend.service.LoginService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController("/api/auth")
@Slf4j
public class LoginController {

    @Autowired
    private LoginService loginService;


    //登录接口
    @PostMapping("login")
    public Result login(@RequestBody LoginPo po) {
        return loginService.login(po);
    }

    @PostMapping("/register")
    public Result register(@RequestBody RegisterPo po) {
        return loginService.register(po);
    }

}
