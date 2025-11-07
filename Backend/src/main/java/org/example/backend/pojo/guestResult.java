package org.example.backend.pojo;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.example.backend.common.constant;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class guestResult {
    private Boolean success;
    private String token;
    private Object trialCount;

    public static guestResult success(String token, Object trialCount) {
        return new guestResult(true, token, trialCount);
    }

    public static guestResult error(){return new guestResult(false, null, null);}
}
