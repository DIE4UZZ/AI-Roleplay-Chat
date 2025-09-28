package org.example.backend.pojo;


import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.example.backend.common.constant;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class Result {

    private Boolean success;

    private String token;
    private Object trialCount;

    //增删改，成功
    public static Result success() {
        return new Result(true, constant.SUCCESS, null);
    }


    public static Result success(Object mes) {return new Result(true, null, null);}

    //查询，成功
    public static Result success(String token ,Object data) {
        return new Result(true, token, data);
    }

    public static Result successLogin(Object data) {return new Result(true, null, data);}

    //失败
    public static Result error(String message) {
        return new Result(false,message, null);
    }
}
