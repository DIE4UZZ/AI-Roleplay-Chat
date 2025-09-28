package org.example.backend.common;


import io.jsonwebtoken.SignatureAlgorithm;
import io.jsonwebtoken.security.Keys;

import javax.crypto.SecretKey;

public interface constant {

    //秘钥
    SecretKey SECRET = Keys.secretKeyFor(SignatureAlgorithm.HS512);


    //成功
    String SUCCESS = "success";

    //失败
    String ERROR = "error";

    //用户名不存在
    String USERNAME_IS_WRONG = "username is wrong";

    //密码错误
    String PASSWORD_IS_WRONG = "password id wrong";

    //邮箱不存在
    String EMAIL_IS_WRONG = "email is wrong";

    //确认密码错误
    String CONFIRM_PASSWORD_DOES_NOT_MATCH = "confirm password does not match";

    //用户名已存在
    String USERNAME_ALREADY_EXISTS = "username already exists";

    //邮箱已存在
    String EMAIL_ALREADY_EXISTS = "email already exists";

    //密码不符合格式
    String PASSWORD_DOES_NOT_MEET_THE_FORMAT_REQUIREMENTS =
            "password does not meet the format requirements";

    //用户名不符合格式
    String USERNAME_DOES_NOT_MEET_THE_FORMAT_REQUIREMENTS =
            "username does not meet the format requirements";

    //邮箱不符合格式
    String EMAIL_DOES_NOT_MEET_THE_FORMAT_REQUIREMENTS =
            "email does not meet the format requirements";

    //Token无效
    String INVALID_TOKEN = "Invalid Token";

    //Token验证失败
    String TOKEN_IS_WRONG = "token is wrong";

    //关键词为空
    String KEYWORD_IS_EMPTY = "keyword is empty";

    //没有这个角色
    String NO_CHARACTER="no character";
}
