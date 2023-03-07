public class drawing {
    public static void drawTriangle(int n) {
int row = 0;

System.out.println('*');
while (row < n) {
    int col = 0;
    while (col < row){
        System.out.print('*');
        col = col +1;
        if (col == row) {
            System.out.println('*');
        }
    }
    
    
    row = row +1;
}
    }
   
    public static void main(String[] args) {
        drawTriangle(16);
    }
}