package org.example.backend.pojo;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class LoginResult {
    private Boolean success;
    private String message;
    private String token;

    public static LoginResult success(String message , String token) {
        return new LoginResult(true ,message, token);
    }

    public static LoginResult success(){return new LoginResult(true,"注册成功",null);}

    public static LoginResult error(){return new LoginResult(false, null, null);}

}
