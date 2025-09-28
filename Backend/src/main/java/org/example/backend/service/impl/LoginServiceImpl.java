package org.example.backend.service.impl;

import org.example.backend.common.JwtUtil;
import org.example.backend.common.constant;
import org.example.backend.mapper.LoginMapper;
import org.example.backend.pojo.LoginPo;
import org.example.backend.pojo.RegisterPo;
import org.example.backend.pojo.Result;
import org.example.backend.pojo.guestResult;
import org.example.backend.service.LoginService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Service;

import java.util.UUID;
import java.util.regex.Pattern;


@Service
public class LoginServiceImpl implements LoginService {
    @Autowired
    private LoginMapper loginMapper;

    @Autowired
    private JwtUtil jwtUtil;

    @Autowired
    private RedisTemplate redisTemplate;

    @Override
    public Result login(LoginPo po) {
        LoginPo user = loginMapper.selectLogin(po);

        if (user == null) {
            LoginPo usernameCheck = new LoginPo();
            usernameCheck.setUsername(po.getUsername());
            LoginPo existUser = loginMapper.selectLogin(usernameCheck);

            if (existUser == null) {
                return Result.error(constant.USERNAME_IS_WRONG);
            } else {
                return Result.error(constant.PASSWORD_IS_WRONG);
            }
        }
        redisTemplate.opsForSet().add(po.getUsername(), -1);
        return Result.successLogin(jwtUtil.generateJwt(po.getUsername(), true));
    }

    @Override
    public Result register(RegisterPo po) {
        //检验输入的密码是否符合8-16位，并且只包含数字和大小写字母
        String regexPassword = "^[A-Za-z0-9]{6,16}$";
        Pattern patternPassword = Pattern.compile(regexPassword);
        //匹配器
        if (!patternPassword.matcher(po.getPassword()).matches()) {
            return Result.error(constant.PASSWORD_DOES_NOT_MEET_THE_FORMAT_REQUIREMENTS);
        }

        //检验用户名是否符合长度大于0小于等于8，并且只包含汉字，数字，大小写字母
        String regexUsername = "^[A-Za-z0-9\u4e00-\u9fa5]{1,8}$";
        Pattern patternUsername = Pattern.compile(regexUsername);
        if (!patternUsername.matcher(po.getUsername()).matches()) {
            return Result.error(constant.USERNAME_DOES_NOT_MEET_THE_FORMAT_REQUIREMENTS);
        }

        //验证用户输入的邮箱是否正确
        String regexEmail = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$";
        Pattern patternEmail = Pattern.compile(regexEmail);
        if (!patternEmail.matcher(po.getEmail()).matches()) {
            return Result.error(constant.EMAIL_DOES_NOT_MEET_THE_FORMAT_REQUIREMENTS);
        }

        //检验用户名是否已经存在
        LoginPo infoUsername = new LoginPo();
        infoUsername.setUsername(po.getUsername());
        if (loginMapper.selectLogin(infoUsername) != null) {
            return Result.error(constant.USERNAME_ALREADY_EXISTS);
        }
        //检验邮箱是否存在
        LoginPo infoEmail = new LoginPo();
        infoEmail.setEmail(po.getEmail());
        if (loginMapper.selectLogin(infoEmail) != null) {
            return Result.error(constant.EMAIL_ALREADY_EXISTS);
        }
        LoginPo info = new LoginPo(infoUsername.getUsername(), po.getPassword(), infoEmail.getEmail());
        loginMapper.register(info);
        return Result.success();
    }

    @Override
    public guestResult guest() {
        String username = UUID.randomUUID().toString();
        int count = 5;
        redisTemplate.opsForHash().put("guest", username, count);
        return guestResult.success(jwtUtil.generateJwt(username, false),1);
    }
}

