package org.example.backend.pojo;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class RegisterPo {
    //用户名
    private String username;

    //登录密码
    private String password;

    //邮箱
    private String email;

    //确认密码
    @JsonProperty("password_again")
    private String passwordAgain;

}
