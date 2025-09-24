package org.example.backend.pojo;


import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class LoginPo{

    //用户名
    private String username;

    //登录密码
    private String password;

    //邮箱
    private String email;

}
