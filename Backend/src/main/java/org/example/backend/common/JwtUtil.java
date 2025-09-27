package org.example.backend.common;

import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import io.jsonwebtoken.security.Keys;
import org.springframework.context.annotation.Configuration;

import javax.crypto.SecretKey;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

import static org.example.backend.common.constant.SECRET;

@Configuration
public class JwtUtil {

    //令牌过期时间 24h
    private static final Long EXPIRATION_TIME = 60*60*1000*24L;


    //生成jwt令牌
     public String generateJwt(String username ,boolean status) {
        Map<String, Object> claims = new HashMap<String, Object>();
        claims.put("username", username);
        claims.put("loginStatus", status);
        return Jwts.builder()
                .setClaims(claims)
                .setSubject(username)
                .setIssuedAt(new Date(System.currentTimeMillis()))
                .setExpiration(new Date(System.currentTimeMillis()+EXPIRATION_TIME))
                .signWith(SignatureAlgorithm.HS512, SECRET)
                .compact();
    }
}
