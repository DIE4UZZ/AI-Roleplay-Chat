package org.example.backend.pojo;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class Character {
    private int id;

    private String name;

    private String Desc;

    private String avatar;

    private String background;
}
