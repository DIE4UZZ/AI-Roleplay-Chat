package org.example.backend.pojo;


import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.example.backend.common.constant;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class Result {

    private int code;
    private String message;
    private Object data;

    //增删改，成功
    public static Result success() {
        return new Result(1, constant.SUCCESS, null);
    }


    public static Result success(String mes) {return new Result(1, mes, null);}

    //查询，成功
    public static Result success(Object data) {
        return new Result(1, constant.SUCCESS, data);
    }

    //失败
    public static Result error(String message) {
        return new Result(-1,message, null);
    }
}
