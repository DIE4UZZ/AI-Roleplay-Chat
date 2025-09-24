package org.example.backend.mapper;

import org.apache.ibatis.annotations.Mapper;
import org.example.backend.pojo.LoginPo;

@Mapper
public interface LoginMapper {

    LoginPo selectLogin(LoginPo po);

    void register(LoginPo info);
}
