program barrier_breach
implicit none

! Allocate variables
integer, parameter :: dp = selected_real_kind(15, 307)
real, allocatable, dimension(:) :: bathy, row
integer :: i, j, mx, my , t1, t2, rowidx, colidx
real :: xll, yll, cellsize, nodata_value, amp_max, dx, sigma, h0, x1, x2, col, stepx, stepy
real :: time(10) != (/(i, i=0,9, 1)/)
real, dimension(10) :: amp
integer, dimension(10) :: zero_array
integer, dimension(10) :: one_array
real, dimension(600) :: y 
real,allocatable, dimension(:,:) :: X_mesh, Y_mesh, breach
real, dimension(500) :: x 
CHARACTER(*), PARAMETER :: fileplace = "/home/claw/clawpack-v5.5.0/geoclaw/scratch/"
! Determine number of increments for X_mesh and Y_mesh
stepx = (100.0 + 100.0)/ 499.0
stepy = (60e3 / 599)

! fill x and y like np.linspace
x = (/((i-1)*stepx -100.0, i=1,500)/)
y = (/((i-1)* stepy + 0, i=1, 600)/)
print *, fileplace//'test.tt3'
! Open bathy file and read header to get size
! OPEN(unit=10, status="old",file=fileplace//"file1.dat")
open(10, file=fileplace//'test.tt3', status='old')
	read(10,*) mx
	read(10,*) my
	read(10,*) xll
	read(10,*) yll
	read(10,*) cellsize
	read(10,*) nodata_value
close(10)

! Declare Amplitude array based on time steps
t1 = 3.0
t2 = 6.0
amp_max = 5.0
dx = 10.0/9.0
time(1:10) = [(0 + ((i-1)*dx),i=1, 10)]

zero_array = 0
one_array = 1

do i = 1, 10
	if (time(i) < t1) then
		amp(i) = zero_array(i)
	elseif (t1 <= time(i) .and. time(i) < t2) then
		amp(i) =  (amp_max / (t2 - t1) * (time(i) - t1))
	elseif (t2 <= time(i)) then
		amp(i) = one_array(i) * amp_max
end if
	
end do
! Open and read bathymetry into memory
! Skip header and declare bathy matrix
allocate(bathy(1:mx*my))
open(11, file='test.tt3')
do i=1,6
    read(11, *)
end do
! Read bathy data into array
do j=1, my !*nrows
   read(11, *) (bathy((j-1)* mx + i),i=1,mx)
end do


! fill x and y matrices a la np.meshgrid
allocate(X_mesh(size(y), size(x)))
allocate(Y_mesh(size(y), size(x)))
do i=1, size(y)
	do j=1, size(x)
		X_mesh(i,j) = x(j)
		Y_mesh(i,j) = y(i)
	end do
end do
! Add breach parameters
x1 = -25.0
x2 = 25.0
sigma = 10.0
h0 = 10.0
allocate(breach(size(X_mesh, 1), size(X_mesh, 2)))
! Initialize breach to match initial height
do i= 1, size(X_mesh,2)
	breach(:,i) = h0
	do j = 1, size(X_mesh,1)
		breach(j,:) = h0
	end do
end do
! Breach the barrier island depending on time
do i = 1, size(amp)
	do rowidx = 1, size(X_mesh, 1)
		row = X_mesh(rowidx,:)
			do colidx = 1, size(X_mesh, 2)
				col = X_mesh(rowidx, colidx)
				if (col >= x1 .and. col <= x2) then
					breach(rowidx, colidx) = breach(rowidx, colidx) & 
					- (amp(i) * exp(-X_mesh(rowidx, colidx)**2/(sigma**2)) &
					* 0.1 * Y_mesh(rowidx, colidx))
				end if
			end do
	end do
end do


end program barrier_breach