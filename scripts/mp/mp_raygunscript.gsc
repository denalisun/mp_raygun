#include common_scripts\utility;
#include maps\mp\_utility;
#include maps\mp\gametypes\_weapon_utils;

init()
{
    precacheitem( "ray_gun_mp" );

    for (;;) {
        level waittill("connected", player);
        //player thread connected();
    }
}

connected() {
    self endon("disconnect");
    for (;;) {
        self waittill("spawned_player");
        self GiveWeapon("ray_gun_zm");
    }
}